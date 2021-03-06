/* Copyright 2014 Mozilla Foundation
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

'use strict';

if (!pdfjsLib.getDocument || !pdfjsViewer.PDFViewer) {
    alert('Please build the pdfjs-dist library using\n' +
        '  `gulp dist-install`');
}

// The workerSrc property shall be specified.
//
pdfjsLib.GlobalWorkerOptions.workerSrc =
    'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.2.228/pdf.worker.js';

// Some PDFs need external cmaps.
//
var CMAP_URL = '';
var CMAP_PACKED = true;
//
// var DEFAULT_URL = 'document/1587';
// var SEARCH_FOR = 'euro'; // try 'Mozilla';

var container = document.getElementById('viewerContainer');

// (Optionally) enable hyperlinks within PDF files.
var pdfLinkService = new pdfjsViewer.PDFLinkService();

// (Optionally) enable find controller.
var pdfFindController = new pdfjsViewer.PDFFindController({
    linkService: pdfLinkService,
});

var pdfViewer = new pdfjsViewer.PDFViewer({
    container: container,
    linkService: pdfLinkService,
    findController: pdfFindController,
});
pdfLinkService.setViewer(pdfViewer);



document.addEventListener('pagesinit', function () {
    // We can use pdfViewer now, e.g. let's change default scale.
    pdfViewer.currentScaleValue = 'page-width';

    if (SEARCH_FOR) { // We can try search for things
        pdfFindController.executeCommand('find', {query: SEARCH_FOR, highlightAll: true});
    }
});

// Loading document.
var loadingTask = pdfjsLib.getDocument({
    url: DEFAULT_URL,
    cMapUrl: CMAP_URL,
    cMapPacked: CMAP_PACKED,
});
loadingTask.promise.then(function (pdfDocument) {
    // Document loaded, specifying document for the viewer and
    // the (optional) linkService.
    pdfViewer.setDocument(pdfDocument);

    pdfLinkService.setDocument(pdfDocument, null);
});

function nextSearch() {
    pdfFindController._nextMatch();
}