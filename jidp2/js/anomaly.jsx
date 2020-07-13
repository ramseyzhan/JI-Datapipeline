import React from 'react';
import PropTypes from 'prop-types';

class Anomaly extends React.Component {
  constructor(props) {
    // Initialize mutable state
    console.log("constructing");
    super(props);
    const { url } = this.props;
    console.log("url in anomaly:", url);
    this.state = { intervalID: 0,nextPage: url, anomalies: [], hasMoreAnomalies: true };
    this.fetchMoreAnomalies = this.fetchMoreAnomalies.bind(this);
  }

  componentDidMount() {
    console.log("didmount");
    const { anomalies, hasMoreAnomalies } = this.state;
    if (anomalies.length === 0) {
      this.fetchMoreAnomalies();
    }
    if (hasMoreAnomalies) {
      this.intervalID = setInterval(this.fetchMoreAnomalies, 1000);
    }
  }

  componentWillUnmount() {
    clearInterval(this.intervalID);
  }

  fetchMoreAnomalies() {
    console.log("fetching");
    const { nextPage } = this.state;
    fetch(nextPage, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        console.log('Response is here:', response);
        return response.json();
      })
      .then((data) => {
        console.log('DEBUG', data);
        this.setState((prevState) => ({
          nextPage: data.next,
          hasMoreAnomalies: data.next !== '',
          anomalies: prevState.anomalies.concat(data.results),
        }));
      })
      .catch((error) => console.log(error));
  }

  render() {
    console.log("rendering")
    const { nextPage, anomalies, hasMoreAnomalies } = this.state;
    return (
      <div className="anomaly">
        {anomalies.map((anomaly) => (
          <span key={anomaly.anomalyid}>
            Time recorded: {anomaly.recorded}, {' '}
            Global active power: {anomaly.global_active_power}, {' '}
            Global reactive power: {anomaly.global_reactive_power}, {' '}
            Voltage: {anomaly.voltage},
            <br/>
            Global intensity: {anomaly.global_intensity}, {' '}
            Sub metering 1: {anomaly.sub_metering_1}, {' '}
            Sub metering 2: {anomaly.sub_metering_2}, {' '}
            Sub metering 3: {anomaly.sub_metering_3}
            <br/>
            <br/>
            <br/>
          </span>
        ))}
      </div>
    );
  }
}

Anomaly.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Anomaly;
