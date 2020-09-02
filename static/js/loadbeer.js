var button = d3.select("#button");
var form = d3.select("#form");
button.on("click", runEnter);
form.on("submit",runEnter);

function runEnter(){
    d3.event.preventDefault();
    var input = getInputValue();

    var filteredData = beer_data.filter(beer => beer.name.toLowerCase().startsWith(input.toLowerCase()));
    $("tbody").html("");
    
    if (filteredData.length === 0) {
        $("tbody").html("No data found.")
    } else {
        Object.entries(filteredData).forEach(([key, value]) => {
            var row = BuildRow(key, value);
            BuildButton(row, value);
        });
    }
};

function BuildButton(row, value) {
    var cell = row.append("td");
    var buttonbeer = cell.append("button").attr("class", "btn btn-secondary");
    // buttonbeer.id = "button-2"
    buttonbeer.text("Show Similar Beers");
    buttonbeer.on("click", function () {
        d3.event.preventDefault();
        alert("Are you ready to see a list of beers you may like? ")
        var tbody = d3.select("tbody");
        $("tbody").html("");
        var cluster_data = beer_data.filter(beer => beer.cluster === value.cluster);
        if (cluster_data.length === 0) {
            $("tbody").html("No data found.")
        } else {
            Object.entries(cluster_data).forEach(([key, value]) => {
                BuildRow(key, value);
            });
        }
    });
}

function BuildRow(key, value) {
    var tbody = d3.select("tbody");
    var row = tbody.append("tr");
    
    BuildColumnData(row, value.name);
    BuildColumnData(row, value.style);
    BuildColumnData(row, value.brewery_name);

    if (value.abv == null) {
        BuildColumnData(row, "--");
    } else {
        BuildColumnData(row, value.abv);
    }
    BuildColumnData(row, value.overall_review)
    BuildColumnData(row, value.taste_review)
    // BuildColumnData(row, value.cluster);
    return row;
    
}

function BuildColumnData(row, value) {
    var cell = row.append("td");
    cell.text(value)
}

var beer_data;
d3.json('/api/beerdata').then(function (data) {
    beer_data = data;
});

function getInputValue() {
    var inputElement = d3.select("#beer-form-input");
    return inputElement.property("value");
}



