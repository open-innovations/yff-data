const firstCharacterInSentence = /(^\w{1}|\.\s*\w{1})/gi;
const firstCharacter = /\w/;
const followingSpaces = /\b\w/g

export const layout = 'layouts/topic.njk';

export default function*({ search }) {
  const topics = (search.values('topics') as string[]).map(s => s.trim());

  for (const topic of topics) {
    const slug = topic.replace(/\W+/g, '-').toLowerCase();

    yield {
      id: slug,
      url: `/topic/${slug}/`,
      title: topic,
      tags: 'topic',
    }
  }
}