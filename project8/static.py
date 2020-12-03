def index():
  return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Apartments Rental Service</title>
    <script src="https://code.jquery.com/jquery-3.5.1.min.js" integrity="sha256-9/aliU8dGd2tb6OSsuzixeV4y/faTqgFtohetphbbj0=" crossorigin="anonymous"></script>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z" crossorigin="anonymous">
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js" integrity="sha384-B4gt1jrGC7Jh4AgTPSdUtOBvfO8shuf57BaghqFfPlYxofvL8/KUEfYiJOMMV+rV" crossorigin="anonymous"></script>
</head>
<body>
<form class="col-6">
    <div class="form-group">
        <label for="apartmentSelect">Апартаменты</label>
        <select class="form-control" id="apartmentSelect">
        </select>
    </div>
    <div class="form-group">
        <label for="countrySelect">Страны</label>
        <select class="form-control" id="countrySelect">
        </select>
    </div>
    <div class="form-group">
        <label for="weekInput">Неделя</label>
        <input type="number" id="weekInput" name="week"></input>
    </div>
</form>
<script lang="js">
    function loadData() {
        const apartmentSelect = $('#apartmentSelect');
        $.getJSON('/apartments', function (apartments) {
           apartments.forEach(function (value) {
               $("<option>").text(value.name).attr("value", value.id)
                   .appendTo(apartmentSelect);
           })
        });
        const countrySelect = $('#countrySelect');
        $.getJSON('/countries', function (countries) {
            countries.forEach(function (value) {
                $("<option>").text(value.name).attr("value", value.id)
                    .appendTo(countrySelect);
            });
        });
    }
    $(document).ready(function () {
        loadData();
    });
</script>
</body>
</html>
  """
