const divisor = function* () {
  let range = 0;
  while(true) {
    for (const base of [1, 2, 5]) yield base * 10**range;
    range++;
  }
};

function calculateStep(range: number) {
  const g = divisor();
  let step = g.next().value;
  while ((range / step) >= 10) {
    step = g.next().value;
  }
  return step;
}

export function generateTickValues(max: number, min=0) {
  const range = max - min;
  const step = calculateStep(range);
  const numTicks = Math.floor(range / step) + 1;

  return Array.from(new Array(numTicks))
    .map((_, i) => i * step + min);
}


export function generateTickArray(axisConfig, data, labelColumn) {
  const tickValues = generateTickValues(axisConfig.max, axisConfig.min);
  const ticks = tickValues.map(v => {
    const index = data.rows.length - 1 - v;
    return {
      value: index,
      label: (typeof data.columns[labelColumn]==="object" ? data.columns[labelColumn][index].replace(/\\n/g, '\n') : "")
    }
  });
  return {
    ...axisConfig,
    ticks,
  }
}            