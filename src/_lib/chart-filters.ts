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


interface generateTickArrayOptions {
  indexFn: (v: number) => number;
  labelColumn?: string;
}

export function generateTickArray(axisConfig, data, options: Partial<generateTickArrayOptions> = {}) {
  const {
    indexFn,
    labelColumn
  }: generateTickArrayOptions = {
    indexFn: (v: number) => v,
    ...options
  };

  const tickValues = generateTickValues(axisConfig.max, axisConfig.min);
  const ticks = tickValues.map(v => {
    const index = indexFn(v);
    return {
      value: index,
      label: (labelColumn && typeof data.columns[labelColumn]==="object" ? data.columns[labelColumn][index].replace(/\\n/g, '\n') : "")
    }
  });
  return {
    ...axisConfig,
    ticks,
  }
}            