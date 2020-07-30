import React from 'react';
import PropTypes from 'prop-types';
import Highchart from './highchart';


class Index extends React.Component {
  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = {
      email: '', threshold: '2', isInput: false, highchartUrl: ''
    };
    this.handleChange = this.handleChange.bind(this);
    this.handleEmailChange = this.handleEmailChange.bind(this);
    this.onFormSubmit = this.onFormSubmit.bind(this);
  }

  componentDidMount() {
    const { url } = this.props;
    const { threshold, isInput } = this.state;
    console.log('INDEX url', url);
    fetch(url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState(() => ({
          threshold,
          isInput,
          highchartUrl: data.highchartUrl,
        }));
      })
      .catch((error) => console.log(error));
  }

  // eslint-disable-next-line react/sort-comp
  handleEmailChange(event) {
    this.setState({
      email: event.target.value,
    });
  }

  handleChange(event) {
    this.setState({
      threshold: event.target.value,
    });
  }

  onFormSubmit(event) {
    event.preventDefault();
    const { url } = this.props;
    const { email, threshold, highchartUrl } = this.state;
    console.log('email: ', email);
    fetch(url,
      {
        method: 'post',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: email, number: threshold }),
        credentials: 'same-origin',
      })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then(() => {
        this.setState({
          email,
          threshold,
          isInput: true,
          highchartUrl,
        });
      })
      .catch((error) => console.log(error));
  }

  render() {
    const {
      email, threshold, isInput, highchartUrl,
    } = this.state;
    if (!isInput) {
      return (
        <div className="index">
          <form onSubmit={this.onFormSubmit}>
            <table>
              <tr>

                <td>Enter email address for alerting messages: </td>
                <td>
                  <input type="text" value={email} onChange={this.handleEmailChange} />
                </td>

                <td>Customize threshold (1 to 10): </td>
                <td>
                  <input type="number" value={threshold} min="1" max="10" step="1" onChange={this.handleChange} />
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
      <div>
        <Highchart url={highchartUrl} />
      </div>
    );
  }
}

Index.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Index;
