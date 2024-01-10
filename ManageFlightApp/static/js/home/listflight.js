document.addEventListener('DOMContentLoaded', function () {
   var btnToggleDetailsList = document.querySelectorAll('.btnToggleDetails');

   btnToggleDetailsList.forEach(function (btnToggleDetails) {
      btnToggleDetails.addEventListener('click', function () {
         var flightId = btnToggleDetails.getAttribute('data-flight-id');
         var ticketClass = btnToggleDetails.getAttribute('class-id');
         var collapseDetails = document.getElementById('collapseDetails' + flightId);

         // Kiểm tra trạng thái hiện tại và thay đổi
         if (collapseDetails.classList.contains('show')) {
            // Nếu đang hiển thị, ẩn đi
            collapseDetails.classList.remove('show');
         } else {
            // Nếu đang ẩn, hiển thị lên
            collapseDetails.classList.add('show');

            // Tại đây, bạn có thể thực hiện bất kỳ xử lý nào khác cho nội dung chi tiết
            // Dựa vào giá trị của ticketClass để xác định hạng vé
         }
      });
   });
});
