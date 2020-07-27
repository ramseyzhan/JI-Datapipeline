import React from 'react';
import PropTypes from 'prop-types';
import Anomaly from './anomaly';

class Index extends React.Component {
  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = { threshold: 2, is_input: false, anomaly: '' };
    this.handleChange = this.handleChange.bind(this);
    this.onFormSubmit = this.onFormSubmit.bind(this);
  }

  componentDidMount() {
    const { url } = this.props;
    const { threshold, is_input } = this.state;
    console.log('INDEX url', url);
    fetch(url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          threshold: threshold,
          is_input: is_input,
          anomaly: data.anomaly,
        });
      })
      .catch((error) => console.log(error));
  }

  handleChange(event) {
    const { anomaly } = this.state;
    this.setState({
      threshold: event.target.threshold,
      is_input: false,
      anomaly: anomaly,
    });
    console.log('is_input: ', this.state.is_input);
  }

  onFormSubmit(event) {
    event.preventDefault();
    const { threshold, anomaly } = this.state;
    this.setState({
      threshold: threshold,
      is_input: true,
      anomaly: anomaly,
    });
    console.log('threshold: ', threshold);
    // TODO: Do something with threshold.
  }

  render() {
    const { threshold, is_input, anomaly } = this.state;
    if (!is_input) {
      return (
        <div className="index">
          <form  onSubmit={this.onFormSubmit}>
            <table>
              <tr>
                <td>Customize threshold (1 to 10): </td>
                <td>
                    <input type="number" value={threshold} min="1" max="10" step="1" onChange={this.handleChange}/>
                    <input type="submit" value="Submit Threshold" />
                </td>
              </tr>
            </table>
          </form>
        </div>
      );
    }
    return (
      <div className="index">
        <Anomaly url={anomaly} />
      </div>
    );
  }
}

Index.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Index;
