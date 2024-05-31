import React from 'react';
import { ReactWidget } from '@jupyterlab/apputils';

function MyComponent(content: string): React.JSX.Element {
  return <div>{content}</div>;
}

export class SimpleWidget extends ReactWidget {
  constructor(c: string) {
    super();
    this.content = c;
  }

  content: string;

  render(): JSX.Element {
    return MyComponent(this.content);
  }
}
