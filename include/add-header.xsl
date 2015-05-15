<?xml version="1.0"?>
<!DOCTYPE xsl:stylesheet [
  <!ENTITY copy   "&#169;" >
  <!ENTITY middot "&#183;" >
]>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
		xmlns:date="http://exslt.org/dates-and-times"
		version="1.0" extension-element-prefixes="date">

  <!-- using encoding="US-ASCII" would make the output compatible with
       both ISO-8859-1 and UTF-8 -->
  <xsl:output method="xml" encoding="UTF-8" indent="yes"
	      omit-xml-declaration="yes"
	      doctype-public="-//W3C//DTD XHTML 1.0 Transitional//EN"
	      doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd" />

  <!-- the root directory for the website -->
  <xsl:param name="root" select="''" />

  <xsl:template match="html">
    <html xmlns="http://www.w3.org/1999/xhtml">
      <xsl:copy-of select="@*" />
      <xsl:apply-templates />
    </html>
  </xsl:template>

  <xsl:template match="head">
    <head xmlns="http://www.w3.org/1999/xhtml">
      <link rel="stylesheet" type="text/css" href="https://www-old.gnome.org/default.css" />
      <link rel="stylesheet" type="text/css" href="https://foundation-old.gnome.org/foundation.css" />
      <link rel="shortcut icon" href="https://sfconservancy.org/favicon.ico" type="image/x-icon" />
      <xsl:copy-of select="@*" />
      <xsl:apply-templates select="node()" />
    </head>
  </xsl:template>

  <xsl:template match="body">
    <body xmlns="http://www.w3.org/1999/xhtml">
      <div id="body">
	<xsl:copy-of select="@*" />
	<xsl:apply-templates select="node()" />
      </div>

      <div id="hdr">
	<div id="logo"><a href="{$root}/"><img src="https://www-old.gnome.org/img/spacer" alt="Home" /></a></div>
        <div id="banner"><img src="https://www-old.gnome.org/img/spacer" alt="" /></div>
	<p class="none"></p>
      </div>

      <!-- Piwik -->
      <script type="text/javascript">
      var pkBaseURL = (("https:" == document.location.protocol) ? "https://webstats.gnome.org/" : "http://webstats.gnome.org/");
      document.write(unescape("%3Cscript src='" + pkBaseURL + "piwik.js' type='text/javascript'%3E%3C/script%3E"));
      </script><script type="text/javascript">
      try {
      var piwikTracker = Piwik.getTracker(pkBaseURL + "piwik.php", 5);
      piwikTracker.trackPageView();
      piwikTracker.enableLinkTracking();
      } catch( err ) {}
      </script><noscript><p><img src="https://webstats.gnome.org/piwik.php?idsite=5" style="border:0" alt=""/></p></noscript>
      <!-- End Piwik Tag -->

    </body>
  </xsl:template>

  <!-- copy elements, adding the XHTML namespace to elements with an
       empty namespace URI -->
  <xsl:template match="*">
    <xsl:choose>
      <xsl:when test="namespace-uri() = ''">
	<xsl:element namespace="http://www.w3.org/1999/xhtml"
		     name="{local-name()}">
	  <xsl:copy-of select="@*" />
	  <xsl:apply-templates select="node()" />
	</xsl:element>
      </xsl:when>
      <xsl:otherwise>
	<xsl:copy>
	  <xsl:copy-of select="@*" />
	  <xsl:apply-templates select="node()" />
	</xsl:copy>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <!-- get rid of processing instructions -->
  <xsl:template match="processing-instruction()">
  </xsl:template>

  <!-- copy everything else -->
  <xsl:template match="node()" priority="-1">
    <xsl:copy>
      <xsl:apply-templates select="node()" />
    </xsl:copy>
  </xsl:template>

</xsl:stylesheet>
