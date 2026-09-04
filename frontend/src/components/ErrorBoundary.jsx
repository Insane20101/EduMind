import React from 'react';

export default class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    this.setState({ error, errorInfo });
    console.error("ErrorBoundary caught an error:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="p-8 m-8 bg-red-50 border border-red-200 rounded-xl" id="error-boundary-ui">
          <h2 className="text-xl font-bold text-red-600 mb-4">Something went wrong.</h2>
          <pre className="bg-white p-4 rounded overflow-auto text-sm text-red-800 border border-red-100 whitespace-pre-wrap">
            {this.state.error && this.state.error.toString()}
            {'\n'}
            {this.state.errorInfo && this.state.errorInfo.componentStack}
          </pre>
        </div>
      );
    }
    return this.props.children;
  }
}
