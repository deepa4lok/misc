============================================
Brand - Report Layout with Background Image
============================================

This module was written to add background image for Brand either in pdf/jpeg format.
Works best on PDF reports, and would work best in combo with report_qweb_pdf_watermark.

Note:
If Background image is inclusive of Header & Footer (Fullpage), then additionally install app report_layout_exclude_header_footer

**Table of contents**

.. contents::
   :local:

Installation
============


As PyPDF is not supported in python3, you need to install PyPDF2::

$ pip install pypdf2

Usage
=====


To use this module, you need to:

#. Go to Settings > Users & Companies > Brands
#. go to your Brand, and add a background image.
#. Next go to Technical Settings > Reports
#. go to your report
#. select a PDF or image to use as watermark. Note that resolutions and size must match, otherwise you’ll have funny results
#. You can also fill in an expression that returns the data (base64 encoded) to be used as watermark


Known Issues
=============


This module has been reported to work with Wkhtmltopdf 0.12.4, and above.
During Bulk docs printing, applies first doc's background image for all.



Credits
=======

Authors
~~~~~~~

* The Open Source Company (TOSC)

Contributors
~~~~~~~~~~~~

* Deepa Venkatesh <deepavenkatesh2015@gmail.com>