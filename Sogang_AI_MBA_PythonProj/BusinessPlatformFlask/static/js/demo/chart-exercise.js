// line chart
/*
c3.generate({
    bindto: '#chart-exercise',
    data: {
      columns: [
        ['data1', 30, 200, 100, 400, 150, 250],
        ['data2', 50, 20, 10, 40, 15, 25]
      ]
    }
});
 */


// bar chart
/*
c3.generate({
    bindto: '#chart-exercise',
    data: {
      columns: [
        ['data1', 30, 200, 100, 400, 150, 250],
        ['data2', 50, 20, 10, 40, 15, 25]
      ],
      type: 'bar'
    }
});
*/

// time series line chart
/*
c3.generate({
    bindto: '#chart-exercise',
    data: {
        x: 'x-axis',
        columns: [
            ['x-axis', '2022-01-01', '2022-01-02', '2022-01-03', '2022-01-04', '2022-01-05', '2022-01-06'],
            ['data1', 30, 200, 100, 400, 150, 250],
            ['data2', 130, 340, 200, 500, 250, 350]
        ]
    },
    axis: {
        x: {
            type: 'timeseries',
            tick: {
                format: '%Y-%m-%d'
            }
        }
    }
});
*/
// pie chart
/*
c3.generate({
    bindto: '#chart-exercise',
    data: {
        columns: [
            ['A', 30],
            ['B', 50],
            ['C', 20],
        ],
        type : 'pie'
    }
});
*/


// donut chart
/*
c3.generate({
    bindto: '#chart-exercise',
    data: {
        columns: [
            ['A', 30],
            ['B', 50],
            ['C', 20],
        ],
        type : 'donut'
    },
    donut: {
        title: "percentage by grade"
    }
});
*/

// gauge chart
/*
c3.generate({
    bindto: '#chart-exercise',
    data: {
        columns: [
            ['data', 90.16]
        ],
        type: 'gauge',
    },
    color: {
        pattern: ['#FF0000', '#F97600', '#F6C600', '#60B044'],
        threshold: {
            values: [30, 60, 90, 100]
        }
    },
});
*/

// line chart button event 1
/*
$("#line-chart-button").click(function(){
    console.log("line-chart-button!!!");
});
*/

// pie chart button event 1
/*
$("#pie-chart-button").click(function(){
    console.log("pie-chart-button!!!");
});
*/

// line chart button event 2
/*
$("#line-chart-button").click(function(){
    c3.generate({
        bindto: '#chart-exercise',
        data: {
          columns: [
            ['data1', 30, 200, 100, 400, 150, 250],
            ['data2', 50, 20, 10, 40, 15, 25]
          ]
        }
    });
});
*/

// pie chart button event 2
/*
$("#pie-chart-button").click(function(){
    c3.generate({
        bindto: '#chart-exercise',
        data: {
            columns: [
                ['A', 30],
                ['B', 50],
                ['C', 20],
            ],
            type : 'pie'
        }
    });
});
*/

// line chart button event 3
/*
$("#line-chart-button").click(function(){
    $.ajax({
        method: "GET",
        url: "/line"
    }).done(function(response) {
        console.log("response data : ");
        console.log(response);
    });
});
*/

// pie chart button event 3
/*
$("#pie-chart-button").click(function(){
    $.ajax({
        method: "GET",
        url: "/pie"
    }).done(function(response) {
        console.log("response data : ");
        console.log(response);
    });
});
*/


// line chart button event 4
/*
$("#line-chart-button").click(function(){
    var chart = c3.generate({
        bindto: '#chart-exercise',
        data: {
            columns: []
        }
    });

    $.ajax({
        method: "GET",
        url: "/line"
    }).done(function(response) {
        chart.load({
          columns: [response]
        });
    });
});
*/

// pie chart button event 4

/*
$("#pie-chart-button").click(function(){
    var chart = c3.generate({
        bindto: '#chart-exercise',
        data: {
            columns: []
        }
    });

    $.ajax({
        method: "GET",
        url: "/pie"
    }).done(function(response) {
         console.log("response data : ");
         console.log(response);
        chart.load({
          columns: [response[0],response[1], response[2]],
          type : 'pie'
        });
    });
});
*/

// ajax 활용
/*
var chart = c3.generate({
    bindto: '#chart-exercise',
    data: {
        columns: []
    }
});

$.ajax({
    method: "GET",
    url: "/pie"
}).done(function(response) {
    chart.load({
      columns: [response[0],response[1], response[2]],
      type : 'pie'
    });
});
 */

var chart = c3.generate({
    bindto: '#chart-exercise',
    data: {
        x: 'x',
        columns: []
    },
    axis: {
        x: {
            type: 'category'
        }
    }
});

$.ajax({
    method: "GET",
    url: "/line"
}).done(function(response) {
    chart.load({
        columns: [
            response[0],  // Places
            response[1]   // Distances
        ]
    });
});