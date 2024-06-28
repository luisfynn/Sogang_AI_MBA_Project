// line chart
/*
c3.generate({
    bindto: '#chart-exercise',
    data: {
      columns: [
        ['data1', 30, 200, 100, 400, 150, 250],
        ['data2', 50, 20, 10, 40, 15, 25],
        ['data3', 70, 100, 120, 80, 150, 90]
      ]
    }
});

//그래프를 그리는 라이브러리 이름이 c3
//html에서 #은 id를 의미함. chart exercise와 연결
*/

// bar chart
/*
c3.generate({
    bindto: '#chart-exercise',
    data: {
      columns: [
        ['data1', 30, 200, 100, 400, 150, 250],
        ['data2', 50, 20, 10, 40, 15, 25],
        ['data3', 70, 100, 120, 80, 150, 90]
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
        x: 'x-axis', //x축에 아래 데이터 넣음, tic을 넣는 방법
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
// c3를 사용하여 게이지 차트 생성
<script>
        // c3를 사용하여 게이지 차트 생성
        var chart = c3.generate({
            bindto: '#chart',
            data: {
                columns: [
                    ['data', 90.16] // 달성률 데이터
                ],
                type: 'gauge'
            },
            gauge: {
                label: {
                    format: function(value, ratio) {
                        return value + '%';
                    },
                    show: true // 달성률 표시 여부
                },
                min: 0, // 최소값
                max: 100, // 최대값
                units: '%' // 단위
            },
            color: {
                pattern: ['#FF0000', '#F97600', '#F6C600', '#60B044'], // 색상 패턴
                threshold: {
                    values: [30, 60, 90, 100] // 임계값
                }
            }
        });
    </script>
//colum data 에 값이 하나만 있는 이유? 게이지 수치
//color: 빨, 주, 노, 초 threshould: 저 구간마다 나눠서 색 나눠서 표시


// line chart button event 1
/*
$("#line-chart-button").click(function(){
    console.log("line-chart-button!!!");
});
*/
//$: 제이쿼리를 사용하라는 표시, $ 넣고 태그 or id or
// id가 line chart button을 클릭하게 되면 아래 명령러를 처리해라.


// pie chart button event 1
/*
$("#pie-chart-button").click(function(){
    console.log("pie-chart-button!!!");
});

//브라우저 화면 콘솔에다가 보여주겠다
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


// pie chart button event 3

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
//a.jax: get 메서드를 사용해서 /pie 라는 url에 request를 보냄.
//요청 보내고 받는건 그냥 request 로 할 수 있지만 서버 응답 기다리는 동안 block됨
//ajax를 이용하면 서버가 명령을 처리하는 동안 기다렸다가 done 되면, response 실행

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