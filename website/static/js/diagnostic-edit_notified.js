document.addEventListener("DOMContentLoaded", function () {
  const notifiedDateInputs = document.querySelectorAll(".edit-date-notified");
  notifiedDateInputs.forEach((input) => {
    const initialDate = input.value ? new Date(input.value) : null;
    new easepick.create({
      element: input,
      css: [
        "https://cdn.jsdelivr.net/npm/@easepick/bundle@1.2.1/dist/index.css",
      ],
      zIndex: 10,
      grid: 1,
      calendars: 1,
      readonly: false,
      format: "MMMM DD, YYYY",
      date: initialDate,
      AmpPlugin: {
        resetButton: true,
      },
      plugins: ["AmpPlugin"],
      setup(picker) {
        picker.on("select", (e) => {
          const selectedDate = e.detail.date;
          input.value = selectedDate.toLocaleDateString("en-US", {
            month: "long",
            day: "numeric",
            year: "numeric",
          });
        });
      },
    });
  });
});
