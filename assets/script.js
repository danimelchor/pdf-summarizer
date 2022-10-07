window.onload = () => {
    var anchors = document.getElementsByTagName("a");

    for (i = 0, len = anchors.length; i < len; i++) {
        anchors[i].addEventListener("click", function (e) {
            e.preventDefault();
            const href = this.getAttribute("href");
            const el = document.getElementById(href.replace("#", ""));
            el.scrollIntoView({
                behavior: "smooth",
                block: "center",
            });
        });
    }
};
