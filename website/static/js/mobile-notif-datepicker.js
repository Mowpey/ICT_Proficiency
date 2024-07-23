const mobile_notif_picker = new Litepicker({
  element: document.getElementById("filter_date_notif_mobile"),
  plugins: ["mobilefriendly", "ranges"],
  mobilefriendly: {
    breakpoint: 991,
  },
});
