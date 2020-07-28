import React from 'react';
import PropTypes from 'prop-types';
import Anomaly from './anomaly';

class Index extends React.Component {
  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = { email: '', threshold: 2, is_input: false, anomaly: '' };
    this.handleChange = this.handleChange.bind(this);
    this.handleEmailChange = this.handleEmailChange.bind(this);
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
        this.setState(() => ({
          threshold: threshold,
          is_input: is_input,
          anomaly: data.anomaly,
        }));
      })
      .catch((error) => console.log(error));
  }

  handleEmailChange(event) {
    this.setState({
      email: event.target.value,
    });
    console.log('is_input: ', this.state.is_input);
  }

  handleChange(event) {
    this.setState({
      threshold: event.target.value,
    });
    console.log('is_input: ', this.state.is_input);
  }

  onFormSubmit(event) {
    event.preventDefault();
    const {url} = this.props;
    const {email, threshold, anomaly} = this.state;
    console.log('email: ', email);
    fetch(url,
      {
        method: 'post',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ text: email, number: threshold }),
        credentials: 'same-origin',
      })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          email: email,
          threshold: threshold,
          is_input: true,
          anomaly: anomaly,
        });
      })
      .catch((error) => console.log(error));
  }

  render() {
    const { email, threshold, is_input, anomaly } = this.state;
    if (!is_input) {
      return (
        <div className="index">
          <form  onSubmit={this.onFormSubmit}>
            <table>
              <tr>

                <td>Enter email address for alerting messages: </td>
                <td>
                    <input type="text" value={email} onChange={this.handleEmailChange}/>
                </td>

                <td>Customize threshold (1 to 10): </td>
                <td>
                    <input type="number" value={threshold} min="1" max="10" step="1" onChange={this.handleChange}/>
                </td>

                <td>
                  <input type="submit" />
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
