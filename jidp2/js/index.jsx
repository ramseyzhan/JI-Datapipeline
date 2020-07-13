import React from 'react';
import PropTypes from 'prop-types';
import Anomaly from './anomaly';

class Index extends React.Component {
  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = { anomaly: '' };
  }

  componentDidMount() {
    const { url } = this.props;
    console.log('INDEX url', url);
    fetch(url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          anomaly: data.anomaly,
        });
      })
      .catch((error) => console.log(error));
  }

  render() {
    const { anomaly } = this.state;
    return (
      <div className="anomalies">
        <Anomaly url={anomaly} />
      </div>
    );
  }
}

Index.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Index;
