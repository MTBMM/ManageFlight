let seatArr = [];
let price = 0;
//
//window.onload = function () {
//    loadOnClick();
//    hideBusi();
//};

function loadOnClick() {
    var listSeat = document.getElementsByClassName('seat-icon-check');
    for (const seat of listSeat) {
        seat.addEventListener("click", e => {
            if (seat.classList.contains("seat-icon-disable")) {
                return;
            }
            ;
            if (seat.classList.contains("seat-icon-empty")) {
                seat.classList.remove("seat-icon-empty");
                seat.classList.add("seat-icon-select");
                toList(seat.getAttribute("value"), 1);
                return;
            }
            if (seat.classList.contains("seat-icon-select")) {
                seat.classList.remove("seat-icon-select");
                seat.classList.add("seat-icon-empty");
                toList(seat.getAttribute("value"), 2);
                return;
            }
        });
    }
}

function hideBusi() {
    document.getElementById("busi-seat").style.display = "none";
    document.getElementById("dex-seat").style.display = "none";
    document.getElementById("eco-seat").style.display = "none";
    document.getElementById("info-pick").style.display = "none";
}

function showAdd() {
        if( document.getElementById("type").value == '2'){
            document.getElementById("busi-seat").style.display = "flex";
    }
}

// script.js
document.addEventListener('DOMContentLoaded', function () {
   {% for f in flights %}
      var btnToggleDetails{{ f.id }} = document.getElementById('btnToggleDetails{{ f.id }}');
      var collapseExample{{ f.id }} = document.getElementById('collapseExample{{ f.id }}');

      btnToggleDetails{{ f.id }}.addEventListener('click', function () {
         // Kiểm tra trạng thái hiện tại và thay đổi
         if (collapseExample{{ f.id }}.classList.contains('show')) {
            // Nếu đang hiển thị, ẩn đi
            collapseExample{{ f.id }}.classList.remove('show');
         } else {
            // Nếu đang ẩn, hiển thị lên
            collapseExample{{ f.id }}.classList.add('show');
         }
      });
   {% endfor %}
});
