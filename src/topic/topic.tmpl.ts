function toTitleCase(str) {
  return str.replace(
    /\w\S*/g,
    function(txt) {
      return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    }
  );
}

export default function*({ search }) {
  const topics = search.values('topics') as string[];

  for (const topic of topics) {
    yield {
      url: `/topic/${topic}/`,
      title: topic.replace(/_/g, ' ').replace(/(^\w{1}|\.\s*\w{1})/gi, (s) => s.toUpperCase()),
      topic: topic,
      tags: 'topic',
    }
  }
}