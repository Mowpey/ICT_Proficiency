if (typeof mobile_exam_picker === "undefined") {
  const mobile_exam_picker = new easepick.create({
    element: "#filter_date_exam_mobile",
    css: ["https://cdn.jsdelivr.net/npm/@easepick/bundle@1.2.1/dist/index.css"],
    zIndex: 10,
    grid: 1,
    calendars: 1,
    readonly: false,
    autoApply: false,
    AmpPlugin: {
      resetButton: true,
    },
    plugins: ["AmpPlugin", "RangePlugin"],
  });
}
