# -*- coding: utf-8 -*-

import datetime
import ftputil
import logging
from odoo import models, fields, api
import base64
import json

try:
    import ftputil.session
except ImportError as e:
    logging.error("ftputil.session could not be imported: %s", e)

_logger = logging.getLogger(__name__)


class FTPConfig(models.Model):
    _name = 'ftp.config'
    _description = 'Connection info of FTP Transfers'

    server = fields.Char(string='Server', help="Servername, including protocol, e.g. https://prod.barneveldsekrant.nl")
    directory = fields.Char(string='Server subdir', help="Directory starting with slash, e.g. /api/v1, or empty")
    tempdir = fields.Char(string='Local temp dir', help="Local temporary directory. e.g. /home/odoo")
    user = fields.Char(string='User')
    password = fields.Char(string='Password')
    latest_run = fields.Char(string='Latest run', help="Date of latest run of Announcement connector", copy=False)
    latest_status = fields.Char(string='Latest status', help="Log of latest run", copy=False)
    output_type = fields.Selection([('csv', 'CSV'), ('xml', 'XML'), ('json', 'JSON')], string='Output File Format',
                                   default='csv')
    active = fields.Boolean(string='Active', default=True)
    description = fields.Char(string='Description')
    sql_export_ids = fields.Many2many('sql.export', 'sql_export_ftp_rel', 'lead_id', 'sql_export_id',
                                      string='SQL Exports')

    def name_get(self):
        return [(rec.id, "%s (%s)" % (rec.server, rec.user)) for rec in self]

    def log_exception(self, msg, final_msg, clear=False):
        for config in self:
            _logger.exception(final_msg)
            config.latest_run = datetime.datetime.utcnow().strftime('UTC %Y-%m-%d %H:%M:%S ')
            if clear:
                config.latest_status = msg + final_msg
            else:
                if not config.latest_status:
                    config.latest_status = ''
                config.latest_status += str('\n ') + msg + final_msg
        return

    def ship_file(self, msg, data, filename):
        for config in self:
            path = config.tempdir + "/"
            try:
                # JSON
                if isinstance(data, dict):
                    with open(path + filename, 'w') as f:
                        json.dump(data, f)
                else:
                    with open(path + filename, "w") as f:
                        f.write(data)
            except Exception as e:
                config.log_exception(msg, f"Invalid Directory, quitting... {e}")
                continue

            # Initiate File Transfer Connection
            try:
                port_session_factory = ftputil.session.session_factory(port=21, use_passive_mode=True)
                ftpServer = ftputil.FTPHost(config.server, config.user, config.password,
                                            session_factory=port_session_factory)
            except Exception as e:
                config.log_exception(msg, f"Invalid FTP configuration, quitting... {e}")
                return False

            try:
                _logger.info("Transferring " + filename)
                target = config.directory or '/'
                source = config.tempdir + '/'
                ftpServer.upload(source + filename, target + filename)
            except Exception as e:
                config.log_exception(msg, f"Transfer failed, quitting.... {e}")
                return False
            finally:
                ftpServer.close()

        return True

    def automated_run(self):
        configurations = self.search([])
        for config in configurations:
            try:
                config.do_send()
            except Exception as e:
                _logger.error("Automated run failed for config %s: %s", config.id, e)

    def do_send(self):
        cursor = self._cr
        msg = ""
        for config in self:
            config.log_exception(msg, '', clear=True)
            if not config:
                config.log_exception(msg, "No configuration found. <br>Please configure FTP connector.")
                continue
            if not config.output_type:
                config.log_exception(msg, "Output Format of the File not defined. <br>Please configure FTP connector.")
                continue
            if not config.server or not config.user or not config.password or not config.tempdir:
                config.log_exception(msg,
                                     "Program not started. <br>Please provide a valid server/user/password/tempdir configuration")
                continue

            sqlExports = config.sql_export_ids.filtered(lambda s: s.state == 'sql_valid')

            if not sqlExports:
                config.log_exception(msg,
                                     "Program not started. <br>Please create a valid record in SQL Export, & ensure it is in 'SQL Valid' state ")
                continue

            GoON = True
            OkFiles = ErrFiles = 0
            for idx, se in enumerate(sqlExports):
                try:
                    if config.output_type == 'xml':
                        query = f"SELECT query_to_xml('{se.query}', true, false, '')"
                        cursor.execute(query)
                        res = cursor.fetchone()[0]
                        filename = f"{se.name}.xml"
                        GoON = config.ship_file(msg, res, filename)
                        if not GoON: return False

                    elif config.output_type == 'csv':
                        wizRec = self.export_sql(sqlExport=se)
                        data = base64.decodebytes(wizRec.binary_file)
                        GoON = config.ship_file(msg, data, wizRec.file_name)
                        if not GoON: return False

                    else:  # JSON
                        cursor.execute(se.query)
                        res = cursor.dictfetchall()
                        data = {'0': res}
                        filename = f"{se.name}.json"
                        GoON = config.ship_file(msg, data, filename)
                        if not GoON: return False

                    OkFiles += 1

                except Exception as e:
                    ErrFiles += 1
                    config.log_exception(msg, f"Error executing SQL ({se.name}) :: {e}")
                    continue

            final_msg = f"File(s) transferred: {OkFiles} Success & {ErrFiles} Failed out of {idx + 1} file(s)..."
            config.log_exception(msg, final_msg)
        return True

    def export_sql(self, sqlExport):
        self.ensure_one()
        wiz = self.env['sql.file.wizard'].create({
            'sql_export_id': sqlExport.id
        })

        variable_dict = {}

        if sqlExport.field_ids:
            for field in sqlExport.field_ids:
                variable_dict[field.name] = self[field.name]
        if "%(company_id)s" in sqlExport.query:
            variable_dict['company_id'] = self.env.user.company_id.id
        if "%(user_id)s" in sqlExport.query:
            variable_dict['user_id'] = self._uid

        res = sqlExport._execute_sql_request(
            params=variable_dict, mode='stdout',
            copy_options=sqlExport.copy_options)

        # Ensure res is a string before encoding
        if isinstance(res, bytes):
            res = res.decode(wiz.sql_export_id.encoding or 'utf-8')

        # Now encode it
        if wiz.sql_export_id.encoding:
            res = res.encode(wiz.sql_export_id.encoding)

        wiz.write({
            'binary_file': res,
            'file_name': sqlExport.name + '.csv'
        })
        return wiz
