function pickPosition(){
    var customerInfo = {
        firstname: document.getElementById('firstname').value,
        lastName: document.getElementById('last-name').value,
        dob: document.getElementById('dob').value,
        gender: document.getElementById('gender').value,
        id: document.getElementsByName('id')[0].value,
        phone: document.getElementsByName('phone')[0].value
    };

    sessionStorage.setItem('customerInfo', JSON.stringify(customerInfo));

    console.log('Thông tin khách hàng: ', customerInfo);
}

function retrieveAndDisplayInfo() {
    // Lấy thông tin khách hàng từ Session Storage
    var storedCustomerInfo = sessionStorage.getItem('customerInfo');

    if (storedCustomerInfo) {
        // Chuyển đổi chuỗi JSON thành đối tượng JavaScript
        var customerInfo = JSON.parse(storedCustomerInfo);

        // Hiển thị thông tin lấy được
        console.log('Thông tin khách hàng:', customerInfo);

        // Thực hiện bất kỳ xử lý nào khác dựa trên thông tin khách hàng
        // Ví dụ: Hiển thị thông tin trên trang web
        displayCustomerInfo(customerInfo);
    } else {
        console.log('Không có thông tin khách hàng trong Session Storage.');
    }
}

function displayCustomerInfo(customerInfo) {
    // Ví dụ: Hiển thị thông tin trên trang web
    alert('Thông tin khách hàng:\n' +
        'First Name: ' + customerInfo.firstname + '\n' +
        'Last Name: ' + customerInfo.lastName + '\n' +
        'Date of Birth: ' + customerInfo.dob + '\n' +
        'Gender: ' + customerInfo.gender + '\n' +
        'CCCD/CMND: ' + customerInfo.id + '\n' +
        'Phone Number: ' + customerInfo.phone);
}