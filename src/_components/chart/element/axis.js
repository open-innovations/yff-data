export const css = `
.axis {
  stroke: black;
  stroke-width: 2px;
}
.axis text {
  font-size: 8px;
}
.x-axis  text {
  text-anchor: middle;
  dominant-baseline: hanging;
}
.y-axis text {
  text-anchor: end;
  dominant-baseline: central;
}
`
export default function ({
  width,
  height,
  offset = 10,
  xLabels = [],
  yLabels = [],
  tickSize = 5,
}) {
  const xLabelPositions = xLabels.map((_, i) => i * width / (xLabels.length - 1));
  const yLabelPositions = yLabels.map((_, i) => i * height / (yLabels.length - 1));
  const xTickPath = xLabelPositions.reduce((a, x) => `${a} M${x} 0 l0 ${-tickSize}`, '');
  const yTickPath = yLabelPositions.reduce((a, y) => `${a} M0 ${y} l${-tickSize} 0`, '');

  let xLabelText = '';
  for (const i in xLabels) {
    const label = `<text x=${xLabelPositions[i]} y=0>${xLabels[i]}</text>`
    xLabelText += label;
  }
  let yLabelText = '';
  for (const i in yLabels) {
    const label = `<text x=0 y=${-yLabelPositions[i]}>${yLabels[i]}</text>`
    yLabelText += label;
  }

  return `<g class="axis">
    <g class="x-axis">
      <line x1=0 y1=${-offset} x2=${width} y2=${-offset}></line>
      <path transform="translate(0 ${-offset})" d="${xTickPath}"/>
      <g transform="scale(1 -1) translate(0 ${offset + tickSize + 5})">${xLabelText}</g>
    </g>
    <g class="y-axis">
      <line x1=${-offset} y1=0 x2=${-offset} y2=${height}></line>
      <path transform="translate(${-offset} 0)" d="${yTickPath}"/>
      <g transform="scale(1 -1) translate(-${offset + tickSize + 5} 0)">${yLabelText}</g>
    </g>
  </g>`;
}