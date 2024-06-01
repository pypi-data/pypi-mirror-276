import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { IMainMenu } from '@jupyterlab/mainmenu';
import { Menu, Widget } from '@lumino/widgets';
import { Dialog, showDialog } from '@jupyterlab/apputils';
import { INotebookTracker } from '@jupyterlab/notebook';
import { IDocumentManager } from '@jupyterlab/docmanager';
import { ICommandPalette } from '@jupyterlab/apputils';
import { IDefaultFileBrowser } from '@jupyterlab/filebrowser';
import { Contents } from '@jupyterlab/services';
import { show_spinner, showFailureImportLabDialog } from '../dialog';
import { MODE, Mode } from '../config';
import { openLab } from '../tools';
import jwt_decode from 'jwt-decode';

const menu: JupyterFrontEndPlugin<void> = {
  id: 'skillsnetwork_jupyter_extension:menu',
  autoStart: true,
  requires: [
    IMainMenu,
    ICommandPalette,
    INotebookTracker,
    IDocumentManager,
    IDefaultFileBrowser
  ],
  activate: async (
    app: JupyterFrontEnd,
    mainMenu: IMainMenu,
    palette: ICommandPalette,
    notebookTracker: INotebookTracker,
    docManager: IDocumentManager,
    fileBrowser: IDefaultFileBrowser
  ) => {
    console.log('skillsnetwork_jupyter_extension:menu extension activated');

    if (MODE === Mode.LEARN) {
      return;
    }

    const { commands } = app;

    const commandID = 'mainMenu:editLabFromToken';
    commands.addCommand(commandID, {
      label: 'Edit a Lab',
      execute: (args: any) => {
        showTokenDialog(
          notebookTracker,
          docManager,
          app.serviceManager.contents,
          fileBrowser
        );
      }
    });

    const category = 'skillsNetwork';
    palette.addItem({
      command: commandID,
      category,
      args: { origin: 'from the palette' }
    });

    // Create a new menu
    const menu: Menu = new Menu({ commands });
    menu.title.label = 'Skills Network';
    mainMenu.addMenu(menu, true, { rank: 80 });

    // Add command to menu
    menu.addItem({
      command: commandID,
      args: {}
    });
  }
};

export default menu;

function showTokenDialog(
  notebookTracker: INotebookTracker,
  docManager: IDocumentManager,
  contentsManager: Contents.IManager,
  fileBrowser: IDefaultFileBrowser
): void {
  // Generate Dialog body
  const bodyDialog = document.createElement('div');
  const nameLabel = document.createElement('label');
  nameLabel.textContent = 'Enter your authorization token';
  const tokenInput = document.createElement('input');
  tokenInput.className = 'jp-mod-styled';
  bodyDialog.appendChild(nameLabel);
  bodyDialog.appendChild(tokenInput);

  showDialog({
    title: 'Edit a Lab',
    body: new Widget({ node: bodyDialog }),
    buttons: [Dialog.cancelButton(), Dialog.okButton()]
  })
    .then(async result => {
      if (result.button.accept) {
        console.log('Token dialog accepted, loading lab...');
        show_spinner('Loading up your lab...');

        const token = tokenInput.value;

        const token_info = jwt_decode(token) as { [key: string]: any };

        let atlas_token = 'NO_TOKEN';
        let awb_token = 'NO_TOKEN';

        if ('version_id' in token_info) {
          console.log('Token contains version_id, opening AWB lab...');
          awb_token = token;
        } else {
          console.log(
            'Token does not contain version_id, opening Atlas lab...'
          );
          atlas_token = token;
        }
        await openLab(
          atlas_token,
          awb_token,
          'Token Launch',
          docManager,
          contentsManager,
          fileBrowser
        );
      }
    })
    .catch(e => {
      Dialog.flush(); //remove spinner
      showFailureImportLabDialog();
      console.error('Error occurred while importing lab:', e);
    });
}
