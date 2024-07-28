document.addEventListener('DOMContentLoaded', function() {
  const examDateInputs = document.querySelectorAll('.edit-date-notified');
  examDateInputs.forEach(input => {
    new easepick.create({
      element: input,
      css: ["https://cdn.jsdelivr.net/npm/@easepick/bundle@1.2.1/dist/index.css"],
      zIndex: 10,
      grid: 1,
      calendars: 1,
      readonly: false,
      format: "MMMM DD, YYYY",
      AmpPlugin: {
        resetButton: true,
      },
      plugins: ["AmpPlugin"],
    });
  });
});
