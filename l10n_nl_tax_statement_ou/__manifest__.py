{
    'name' : 'Integrate Netherlands BTW Statement & Operating Unit',
    'version': '14.0.1.0.0',
    'category': 'Localization',
    'author'  : "The Open Source Company",
    'website' : 'http://www.tosc.nl',
    'depends' : ['l10n_nl_tax_statement','operating_unit'],
    'data' : ["views/l10n_nl_vat_statement.xml",
              "report/report_tax_statement.xml"],
    'installable': True
}
