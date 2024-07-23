if (typeof notif_picker === "undefined") {
  const notif_picker = new easepick.create({
    element: "#filter_date_notif",
    css: ["https://cdn.jsdelivr.net/npm/@easepick/bundle@1.2.1/dist/index.css"],
    zIndex: 10,
    grid: 1,
    calendars: 1,
    readonly: false,
    AmpPlugin: {
      resetButton: true,
    },
    plugins: ["AmpPlugin", "RangePlugin"],
  });
}
