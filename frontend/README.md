# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react/README.md) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh


<!-- 
creation =>
npm install -g yarn
npm install -g vite
npm create vite@latest . -- --template react ( le point veux dire crée le projet dans le repertoire frontend ou on se trouve )
remplire le fichier le fichier package.json (supprimes ce qui a été avant et copies cel dans github))
executer yarn et le node_module sera telecherger
pour lancer le serveur executer: yarn dev

--------------------------------------------------------------------------

pour isnatller saas : yarn global add sass
verifier ou yarn stock les paquets globaux

--------------------------------------------------------------------------
// npm install styled-components => permet de créer des styled component
import styled from 'styled-components';
import { Link } from 'react-router-dom';

const NoUnderlineLink = styled(Link)`
  text-decoration: none;
`;

<NoUnderlineLink to="/some-path">Your Link Text</NoUnderlineLink>
 -->