<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Page Title</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
    <script>
let xhttp = new XMLHttpRequest();

xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
       console.log(xhttp.responseText);
    }
};

xhttp.open("POST", "http://127.0.0.1:5000", true);
xhttp.send("POST data");

</script>
</body>
</html>

