<!DOCTYPE html>
<meta charset="utf-8">
<title>Zoomable Treemaps with Color</title>
<style>

@import url(../style.css?aea6f0a);

#chart {
  width: 960px;
  height: 500px;
}

text {
  pointer-events: none;
}

.grandparent text {
  font-weight: bold;
}

rect {
/*  fill: none; */
  stroke: #fff;
  stroke-width: 1px;
}

rect.parent,
.grandparent rect {
  stroke-width: 2px;
}

.grandparent:hover rect {
  fill: darkgrey;
}

.children rect.parent,
.grandparent rect {
  cursor: pointer;
}

.children rect.child {
  opacity: 0;
}

.children rect.parent {
}

.children:hover rect.child {
  opacity: 1;
  stroke-width: 1px;
}

.children:hover rect.parent {
  opacity: 0;
}

.legend rect {
  stroke-width: 0px;
}

.legend text {
  text-anchor: middle;
  pointer-events: auto;
  font-size: 15px;
  font-family: sans-serif;
  fill: black;
}

</style>

<header>
  <aside>Adapted from Mike Bostock's <a href="http://bost.ocks.org/mike/treemap/">Zoomable Treemaps</a></aside>
</header>

<h1>Zoomable Treemaps, with Color</h1>
<p>Hover on any cell to see next level of detail, or click on a cell to zoom in. Click on the top label to zoom out.</p>
<p id="chart">
<h3 style="font-weight: bold">Legend</h3>
<p style="width: 960px">Color: Percent change in number of cases of TB from 2006 to 2012 (negative is good).</p>
<div id="legend"></div>
<p>Size of box: number of TB cases in 2012.</p>

<footer>
  <h3>References</h3>
  <aside>Data from US Center for Disease Control <a href="http://wonder.cdc.gov/TB-v2012.html">Wonder database</a>.</aside>
  <aside>Original <a href="http://bost.ocks.org/mike/treemap/">treemap</a> created June, 2012 by Mike Bostock.  Adapted by Zan Armstrong in Sept 2014.</aside>
</footer>

<script src="https://d3js.org/d3.v3.min.js"></script>
