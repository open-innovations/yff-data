export function transpose(matrix) {
  return matrix[0].map((_, colIndex) => matrix.map(row => row[colIndex]));
}

export function range(array) {
  return {
    min: Math.min(...array.filter(x => x)),
    max: Math.max(...array.filter(x => x)),
  };
}

export function loadDataFile(path, sources) {
  const name = path.replace(/\//g, '.').replace(/^.*data/, 'sources').replace(/\.[^\.]*$/, '');
  return eval(name);
}
