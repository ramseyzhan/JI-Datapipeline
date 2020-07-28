import React from 'react';
import PropTypes from 'prop-types';

class Anomaly extends React.Component {
  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = { anomalies: [] };
  }

  componentDidMount() {
    // This line automatically assigns this.props.url to the const variable url
    const { url } = this.props;

    // Call REST API to get number of likes
    fetch(url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          anomalies: data.anomalies
        });
      })
      .catch((error) => console.log(error));
  }

  render() {
    const{ anomalies } = this.state;
  }
}

Anomaly.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Anomaly;
