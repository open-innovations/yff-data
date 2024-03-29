export const css = `
  .scatter-chart {
    width: 100%;
    stroke-linecap: round;
  }
  .scatter-chart * {
    vector-effect: non-scaling-stroke;
  }
  .scatter-chart text {
    stroke: none;
  }
`
export default function ({ content, width, height, margin, id }) {
  return `<svg id=${id || crypto.randomUUID()}
    class="chart scatter-chart"
    viewBox="-${margin} -${margin} ${width + 2 * margin} ${height + 2 * margin}" 
    xmlns="http://www.w3.org/2000/svg" >
      ${ content }
    </svg>`;
}