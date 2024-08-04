if (typeof notif_picker === "undefined") {
  const notif_picker = new easepick.create({
    element: "#sort_date_notified",
    css: ["https://cdn.jsdelivr.net/npm/@easepick/bundle@1.2.1/dist/index.css"],
    zIndex: 10,
    grid: 1,
    calendars: 1,
    readonly: false,
    format: "MMMM DD, YYYY",
    AmpPlugin: {
      resetButton: true,
    },
    plugins: ["AmpPlugin", "RangePlugin"],
  });
}
