<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:s="http://www.w3.org/2000/svg" version="1.0">
    <xsl:param name="backColor" select="'34495d'"/>
    <xsl:param name="paperColor" select="'ffffff'"/>
    <xsl:param name="frontColor" select="'1abc9c'"/>
    <xsl:output indent="yes"/>
    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>
    <xsl:template match="//s:rect[@id = 'folderTab']">
        <xsl:copy>
            <xsl:apply-templates select="@*"/>
            <xsl:attribute name="style">
                <xsl:value-of select="concat('fill:#', $backColor, ';fill-opacity:1;stroke:none')"/>
            </xsl:attribute>
        </xsl:copy>
    </xsl:template>
    <xsl:template match="//s:rect[@id = 'folderBackground']">
        <xsl:copy>
            <xsl:apply-templates select="@*"/>
            <xsl:attribute name="style">
                <xsl:value-of select="concat('fill:#', $backColor, ';fill-opacity:1;stroke:none')"/>
            </xsl:attribute>
        </xsl:copy>
    </xsl:template>
    <xsl:template match="//s:rect[@id = 'folderPaper']">
        <xsl:copy>
            <xsl:apply-templates select="@*"/>
            <xsl:attribute name="style">
                <xsl:value-of select="concat('fill:#', $paperColor, ';fill-opacity:1;stroke:none')"/>
            </xsl:attribute>
        </xsl:copy>
    </xsl:template>
    <xsl:template match="//s:rect[@id = 'folderFront']">
        <xsl:copy>
            <xsl:apply-templates select="@*"/>
            <xsl:attribute name="style">
                <xsl:value-of select="concat('fill:#', $frontColor, ';fill-opacity:1;stroke:none')"/>
            </xsl:attribute>
        </xsl:copy>
    </xsl:template>
    
</xsl:stylesheet>
