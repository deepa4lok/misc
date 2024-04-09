# -*- coding: utf-8 -*-

{
    "name": "Brand - Pdf Background Image [Deprecated]",
    "version": "14.0.1.0.1",
    "author": "Deepa, " "The Open Source company (TOSC)",
    "license": "AGPL-3",
    "category": "Technical Settings",
    "summary": "Adds background image to your PDF reports as per Brand"
               "Originally this app was built to overcome the drawback of the original app, report_qweb_pdf_watermark, "
               "However it has been found, that the latter module works well with correct Wkhtmltopdf 0.12.4 or above, "
               "hence this app will be deprecated",
    "website": "https://tosc.nl",
    "depends": ["web", "brand",
                "report_qweb_pdf_bgimage"
                ],
    "data": [
        "views/res_brand_view.xml",
    ],
    "installable": True,
}
