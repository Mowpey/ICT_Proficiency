const mobile_exam_picker = new Litepicker({
  element: document.getElementById("filter_date_exam_mobile"),
  plugins: ["mobilefriendly", "ranges"],
  mobilefriendly: {
    breakpoint: 991,
  },
});
