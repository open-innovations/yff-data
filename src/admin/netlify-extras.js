window.addEventListener('DOMContentLoaded', () => {
  const DEFAULT_SEPARATOR = ',';

  const CategoriesControl = createClass({
    handleChange: function (e) {
      const separator = this.props.field.get('separator', DEFAULT_SEPARATOR);
      this.props.onChange(e.target.value.split(separator).map((e) => e));
    },

    render: function () {
      const separator = this.props.field.get('separator', DEFAULT_SEPARATOR);
      var value = this.props.value;
      return h('input', {
        id: this.props.forID,
        className: this.props.classNameWrapper,
        type: 'text',
        value: value ? value.join(separator) : '',
        onChange: this.handleChange,
      });
    },
  });

  const CategoriesPreview = createClass({
    render: function () {
      return h(
        'ul',
        {},
        this.props.value.map(function (val, index) {
          return h(
            'li',
            {
              key: index,
            },
            val
          );
        })
      );
    },
  });

  const schema = {
    properties: {
      separator: {
        type: 'string',
      },
    },
  };

  CMS.registerWidget(
    'categories',
    CategoriesControl,
    CategoriesPreview,
    schema
  );
});
