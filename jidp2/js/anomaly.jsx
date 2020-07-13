import React from 'react';
import PropTypes from 'prop-types';
import Index from './index';

class Anomaly extends React.Component {
  constructor(props) {
    // Initialize mutable state
    super(props);
    const { url } = this.props;
    this.state = { nextPage: url, anomalies: [], hasMoreAnomalies: true };
  }

  componentDidMount() {
    const { anomalies } = this.state;
    if (anomalies.length === 0) {
      this.fetchMoreAnomalies();
    }
  }

  fetchMoreAnomalies() {
    const { nextPage } = this.state;
    fetch(nextPage, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState((prevState) => ({
          nextPage: data.next,
          hasMoreAnomalies: data.next !== '',
          anomalies: prevState.anomalies.concat(data.results),
        }));
      })
      .catch((error) => console.log(error));
  }

  render() {
    const { nextPage, anomalies, hasMoreAnomalies } = this.state;
    return (
      <div>
        {anomalies.map((anomaly) => (
          <span key={anomaly.anomalyid}>
            Date;Time;Global_active_power;Global_reactive_power;Voltage;Global_intensity;Sub_metering_1;Sub_metering_2;Sub_metering_3
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
