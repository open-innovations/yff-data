export const css = `
.scatter-chart .line {
  fill: none;
  stroke-width: 2px;
}
`;

const scaler = ({ axis, width, height }) => {
  const xMin = axis?.x.min || 0;
  const yMin = axis?.y.min || 0;
  const xMax = axis?.x.max || 1;
  const yMax = axis?.y.max || 1;
  return ([x, y]) => [
    (x / xMax - xMin) * width,
    (y / yMax - yMin) * height,
  ];
}

export default function ({
  axis,
  series,
  pointSize = 3,
  comp,
}) {
  const margin = 40;
  const width = 400;
  const height = 200;

  const normalisePoints = scaler({ axis, width, height });
  const pointToSvg = (colour) => ([x, y]) => `<circle id="point" style="fill: ${colour}" cx=${x} cy=${y} r=${pointSize} />`;
  const pointsToPath = (a, [x, y], i) => (i == 0) ? `M${x} ${y}` : `${a} L${x} ${y}`;

  const chartData = series.map((s) => ({
    ...s,
    points: s.points.map(normalisePoints),
    colour: s.colour || '#fff',
  }));

  const seriesPlots = chartData.map(({ name, points, colour, line = true }) => {
    return `<g class="series" id="${name}">
      ${(line ? `<path class="line" style="stroke: ${colour}" d="${points.reduce(pointsToPath, '')}"/>` : '') +
      points.map(pointToSvg(colour)).join('')
      }
    </g>`;
  }).join('\n');

  const content = `<g transform="translate(0 ${height}) scale(1 -1)" >
      ${comp.chart.element.axis({ width, height, xLabels: axis.x?.ticks, yLabels: axis?.y?.ticks, offset: axis?.offset })}
      ${seriesPlots}
    </g>`;
  return comp.chart.element.wrapper({ content, width, height, margin });
}