import React from 'react';
import PropTypes from 'prop-types';
import reactMixin from 'react-mixin';
import autoBind from 'react-autobind';
import Reflux from 'reflux';
import Dropzone from 'react-dropzone';
import Select from 'react-select';
import {bem} from 'js/bem';
import {LoadingSpinner} from 'js/ui';
import {stores} from 'js/stores';
import mixins from 'js/mixins';
import {renderBackButton} from './modalHelpers';
import {validFileTypes} from 'utils';
import {ASSET_TYPES} from 'js/constants';

const DESIRED_TYPES = [
  {
    value: ASSET_TYPES.block.id,
    label: ASSET_TYPES.block.label,
  },
  {
    value: ASSET_TYPES.template.id,
    label: ASSET_TYPES.template.label,
  },
];

class LibraryUploadForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      isSessionLoaded: !!stores.session.currentAccount,
      isPending: false,
      // default is block
      desiredType: DESIRED_TYPES[0],
    };

    autoBind(this);
  }

  componentDidMount() {
    this.listenTo(stores.session, () => {
      this.setState({isSessionLoaded: true});
    });
  }

  onFileDrop(files, rejectedFiles, evt) {
    // TODO:
    // 1. add button for submitting the file
    // 2. when file is uploaded, do nothing, let user submit the form
    // 3. if modal opened and file was passed, make it being selected
    console.log('onFileDrop', files, rejectedFiles, evt);
    // append desiredType to the asset
    if (files[0]) {
      files[0].desiredType = this.state.desiredType.value;
    }
    this.setState({isPending: true});
    // 4. make the rejection better - isPending: false
    this.dropFiles(files, rejectedFiles, evt);
  }

  onDesiredTypeChange(newValue) {
    this.setState({desiredType: newValue});
  }

  render() {
    if (!this.state.isSessionLoaded) {
      return (<LoadingSpinner/>);
    }

    return (
      <bem.FormModal__form className='project-settings project-settings--upload-file'>
        <bem.Modal__subheader>
          {t('Import an XLSForm from your computer.')}
        </bem.Modal__subheader>

        {!this.state.isPending &&
          <React.Fragment>
            <bem.FormModal__item>
              <label htmlFor='desired-type'>
                {t('Choose desired type')}
              </label>

              <Select
                id='desired-type'
                value={this.state.desiredType}
                onChange={this.onDesiredTypeChange}
                options={DESIRED_TYPES}
                className='kobo-select'
                classNamePrefix='kobo-select'
                menuPlacement='auto'
              />
            </bem.FormModal__item>

            <bem.FormModal__item>
              <Dropzone
                onDrop={this.onFileDrop.bind(this)}
                multiple={false}
                className='dropzone'
                activeClassName='dropzone-active'
                rejectClassName='dropzone-reject'
                accept={validFileTypes()}
              >
                <i className='k-icon-xls-file' />
                {t(' Drag and drop the XLSForm file here or click to browse')}
              </Dropzone>
            </bem.FormModal__item>
          </React.Fragment>
        }
        {this.state.isPending &&
          <div className='dropzone'>
            <LoadingSpinner message={t('Uploading file…')}/>
          </div>
        }

        <bem.Modal__footer>
          {renderBackButton(this.state.isPending)}
        </bem.Modal__footer>
      </bem.FormModal__form>
    );
  }
}

reactMixin(LibraryUploadForm.prototype, Reflux.ListenerMixin);
reactMixin(LibraryUploadForm.prototype, mixins.droppable);
LibraryUploadForm.contextTypes = {router: PropTypes.object};

export default LibraryUploadForm;
