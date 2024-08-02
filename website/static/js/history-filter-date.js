document.addEventListener('DOMContentLoaded', function() {
    const dateInput = document.getElementById('date');
    const initialValue = dateInput.value;
  
    const exam_picker = new easepick.create({
      element: dateInput,
      css: ["https://cdn.jsdelivr.net/npm/@easepick/bundle@1.2.1/dist/index.css"],
      zIndex: 10,
      grid: 2,
      calendars: 2,
      readonly: false,
      format: "MMM DD, YYYY",
      plugins: ["RangePlugin"],
      RangePlugin: {
        tooltip: true,
      },
      setup(picker) {
        if (initialValue) {
          const [start, end] = initialValue.split(' - ');
          picker.setDateRange(start, end);
        }
  
        picker.on('select', (e) => {
          const { start, end } = e.detail;
          dateInput.value = start && end ? `${start.format('MMM DD, YYYY')} - ${end.format('MMM DD, YYYY')}` : '';
        });
      }
    });
  
  });

  