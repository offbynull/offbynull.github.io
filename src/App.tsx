import * as React from 'react';
// import ReactDOM from 'react-dom'
import * as Immutable from 'immutable';
import * as t from "io-ts";
import './App.css';
import { Logo } from './Logo';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faMapMarkerAlt, faEnvelope } from '@fortawesome/free-solid-svg-icons';
import { faGithub } from '@fortawesome/free-brands-svg-icons';
import { FinishedStudyList, FinishedStudyEntryV } from './FinishedStudyList';
import { PendingStudyEntryV, PendingStudyList } from './PendingStudyList';
import { fold } from 'fp-ts/lib/Either';
import { pipe } from 'fp-ts/lib/function';

export interface AppProps {
}

export interface AppState {
  readonly data: AppData | undefined
}

export class App extends React.Component<AppProps, AppState> {
  public constructor(props: AppProps, context?: any) {
    super(props, context);
    this.state = {
      data: undefined
    };
  }

  public componentDidMount() {
    (async () => {
      const resp = await fetch('data/data.json', { cache: 'no-cache' });
      const obj = await resp.json();
      const ret = pipe(
        AppDataV.decode(obj),
        fold(
          errors => {
            console.log(errors)
            throw new Error(JSON.stringify(errors));
          },
          value => value,
        ),
      );

      this.setState({
        data: ret
      });
    })();
  }

  public render() {
    return (
      <div className="App">
        <div className="logo">
          <Logo />
        </div>
        <div className="name">
          Kasra Faghihi
        </div>
        <div className="info">
          <span className="item"><FontAwesomeIcon icon={faGithub} />&nbsp;<a href="https://www.github.com/offbynull">offbynull</a></span>
          <span className="item"><FontAwesomeIcon icon={faEnvelope} />&nbsp;<a href="mailto:offbynull@gmail.com">offbynull@gmail.com</a></span>
          <span className="item"><FontAwesomeIcon icon={faMapMarkerAlt} />&nbsp;Cambridge,&nbsp;MA</span>
        </div>
        <div className="nav">
          <span className="item"><a href="#study_notes">notes</a></span>
          <span className="item"><a href="#study_backlog">backlog</a></span>
          <span className="item"><a href="data/learn/Anki/output/output.html">anki</a></span>
        </div>
        <h1 id="study_notes">notes</h1>
        <div>Personal notes from past and current books / online courses / self-studies.</div>
        {this.state.data === undefined ? <div>Loading...</div> : <FinishedStudyList notes={Immutable.List(this.state.data.finishedStudyList)} />}
        <h1 id="study_backlog">backlog</h1>
        <span>Personal backlog of books / courses / etc..</span>
        {this.state.data === undefined ? <div>Loading...</div> : <PendingStudyList notes={Immutable.List(this.state.data.pendingStudyList)} />}
      </div>
    );
  }
}

export const AppDataV =
  t.readonly(
    t.type({
      finishedStudyList: t.readonlyArray(FinishedStudyEntryV),
      pendingStudyList: t.readonlyArray(PendingStudyEntryV)
    })
  );

export type AppData = t.TypeOf<typeof AppDataV>;
