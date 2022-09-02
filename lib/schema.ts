export const ReportSchema = {
  $schema: 'http://json-schema.org/draft-07/schema#',
  $id: 'https://yff.open-innovations.org/report.schema.json',
  title: 'ReportSchema',
  description: 'A report published on the Youth Futures Foundation data portal',

  type: 'object',
  required: ['title'],
  properties: {
    title: {
      type: 'string',
    },
    draft: {
      type: 'boolean',
    },
    publication_date: {
      // type: 'string',
      // format: 'date',
    },
    summary: {
      type: 'array',
      items: {
        type: 'string',
      },
    },
    visualisations: {
      type: 'array',
      items: {
        $ref: '#/$defs/visualisationTypes',
      },
    },
    report_link: {
      type: 'string',
    },
    sections: {
      type: 'array',
      items: { $ref: '#/$defs/section' },
    },
  },
  additionalProperties: false,
  $defs: {
    block: {
      type: 'object',
      additionalProperties: false,
      properties: {
        title: { type: 'string' },
        caption: { type: 'string' },
        visualisations: {
          type: 'array',
          items: {
            $ref: '#/$defs/visualisationTypes',
          },
        },
        featured_block: { type: 'boolean' },
        text: { type: 'string', nullable: true },
      },
    },
    link: {
      type: 'object',
      properties: {
        title: {
          type: 'string',
        },
        link: {
          type: 'string',
        },
      },
    },
    section: {
      type: 'object',
      properties: {
        title: {
          type: 'string',
        },
        summary: {
          type: 'string',
        },
        tags: {
          type: 'array',
          description: 'Topics covered by the section',
          items: { type: 'string' },
        },
        blocks: {
          type: 'array',
          items: { $ref: '#/$defs/block' },
        },
      },
      additionalProperties: false,
    },
    visualisationTypes: {
      // unevaluatedProperties: false,
      allOf: [
        {
          type: 'object',
          properties: {
            title: { type: 'string' },
            caption: { type: 'string' },
            tab: { type: 'string' },
            citations: { type: 'array', items: { $ref: '#/$defs/link' } },
          },
        },
        {
          oneOf: [
            {
              type: 'object',
              title: 'Static Image',
              properties: {
                type: {
                  const: 'static-image',
                },
                config: {
                  type: 'object',
                  properties: {
                    link: { type: 'string' },
                    description: { type: 'string' },
                  },
                  additionalProperties: false,
                },
              },
            },
            {
              type: 'object',
              properties: {
                type: { const: 'dashboard' },
                config: {
                  type: 'object',
                  properties: {
                    file: {},
                    title: {},
                    value: {},
                    note: {},
                    width: {},
                    units: {},
                    panels: {},
                  },
                  additionalProperties: false,
                },
              },
            },
            {
              type: 'object',
              properties: {
                type: { const: 'table' },
                config: {
                  type: 'object',
                  properties: {
                    file: {},
                    columns: {},
                  },
                  additionalProperties: false,
                },
              },
            },
            {
              type: 'object',
              properties: {
                type: { const: 'chart' },
                config: {
                  type: 'object',
                  properties: {
                    file: {},
                    summary: {},
                    type: { enum: ["stacked-bar-chart"] },
                    legend: { type: 'object' },
                    axis: { type: 'object' },
                    category: {},
                    series: { type: 'array' },
                  },
                  additionalProperties: false,
                },
              },
            },
          ],
        },
      ],
    },
  },
};
