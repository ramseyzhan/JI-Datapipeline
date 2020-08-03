import React from 'react';
import PropTypes from 'prop-types';
// Import Highcharts
import Highcharts from "highcharts/highstock";
import HighchartsReact from "highcharts-react-official";
import HC_more from "highcharts/highcharts-more"; //module
HC_more(Highcharts); //init module

class MyChart extends React.Component {
  constructor(props) {
    console.log('initialized');
    super(props);
    this.state = {
      series: [
        {
          name: 'actual val',
          data: []
        },
        {
          name: 'predic clstm',
          data: []
        },
        {
          name: 'predic traditional lstm',
          data: []
        },
        {
          type: 'scatter',
          color: 'rgba(255, 0, 0, 1)',
          name: 'abnormal',
          data: []
        }
      ]
    };
  }

  componentDidMount() {
    const {url} = this.props;
    fetch(url,
      {
        method: 'post',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({'url' : window.location.href }),
        credentials: 'same-origin',
      })
      .then((response) => {
        console.log(response);
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        console.log('data');
        console.log(data);
        this.setState(() => ({
          series: [{
            name: 'actual val',
            data: data.all_data
          },
            {
              name: 'predic clstm',
              data: data.predic_clstm
            },
            {
              name: 'predic traditional lstm',
              data: data.predic_traditional
            },
            {
              type: 'scatter',
              color: 'rgba(255, 0, 0, 1)',
              name: 'abnormal',
              data: data.abnormal_data
            }]
        }));

      })
      .catch((error) => console.log(error));
  }

  render() {
    console.log('rendering');
    const {series} = this.state;
    console.table(series);


    var title = "IBM Stock Price";
    var local_arr= window.location.href.split('/');
    if(local_arr[local_arr.length - 1]=='Power'){
      title= 'Power Usage'
    }

    return (
      <div>
        <HighchartsReact
          constructorType={"stockChart"}
          // ref={this.chartComponent}
          highcharts={Highcharts}
          options={{
            title: {
              text: title
            },

            exporting: {
              enabled: false
            },

            chart: {
              zoomType: 'x'
            },

            xAxis: {
              type: 'datetime',
              dateTimeLabelFormats: {
                millisecond: '%H:%M:%S.%L',
                second: '%H:%M:%S',
                minute: '%H:%M',
                hour: '%H:%M',
                day: '%m-%d',
                week: '%m-%d',
                month: '%Y-%m',
                year: '%Y'
              }
            },

            yAxis: {
              title: {
                text: 'Power Usage'
              }
            },

            tooltip: {
              dateTimeLabelFormats: {
                millisecond: '%H:%M:%S.%L',
                second: '%H:%M:%S',
                minute: '%H:%M',
                hour: '%H:%M',
                day: '%Y-%m-%d',
                week: '%m-%d',
                month: '%Y-%m',
                year: '%Y'
              }
            },

            legend: {
              enabled: true
            },

            plotOptions: {
              area: {
                fillColor: {
                  linearGradient: {
                    x1: 0,
                    y1: 0,
                    x2: 0,
                    y2: 1
                  },
                  stops: [
                    [0, new Highcharts.getOptions().colors[0]],
                    [1, new Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                  ]
                },
                marker: {
                  radius: 2
                },
                lineWidth: 1,
                states: {
                  hover: {
                    lineWidth: 1
                  }
                },
                threshold: null
              }
            },

            series: series
          }}
        />
      </div>
    );
  }
}

MyChart.propTypes = {
  url: PropTypes.string.isRequired,
};

export default MyChart;
