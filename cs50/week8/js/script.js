document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('window-top').addEventListener('click', function () {
        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
    });

})