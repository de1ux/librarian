import { useEffect, useState } from "react";
import { useLocation } from "react-router";
import { DocumentModel } from "../models/Document";
import { Link } from "react-router-dom";
import { DocumentTextModel } from "../models/DocumentText";
import { Api } from "../utils/Api";

function useQuery() {
  return new URLSearchParams(useLocation().search);
}

function Search() {
  const [documentSearch, setDocumentSearch] = useState([]);
  const [documentTextSearch, setDocumentTextSearch] = useState([]);
  const query = useQuery();
  const q = query.get("q");
  const api = new Api();

  useEffect(() => {
    api.searchDocumentTitles(q).then((d) => setDocumentSearch(d.data));
    api.searchDocumentText(q).then((d) => setDocumentTextSearch(d.data));
  }, [q]);

  const formatDocumentLinks = (links: Array<DocumentModel>) => {
    return (
      <ul>
        {links.map((l) => {
          return (
            <li>
              <Link to={`/folders/${l.folder}/documents/${l.id}`}>
                {l.filename}
              </Link>
            </li>
          );
        })}
      </ul>
    );
  };

  const formatDocumentTextLinks = (links: Array<DocumentTextModel>) => {
    return (
      <ul>
        {links.map((l) => {
          return (
            <li>
              <Link
                to={`/folders/${l.folder}/documents/${l.document}/pages/${
                  l.page_number + 1
                }`}
              >
                {l.text}
              </Link>
            </li>
          );
        })}
      </ul>
    );
  };

  return (
    <div>
      <h1>Document Search</h1>
      {documentSearch.length ? (
        <div>{formatDocumentLinks(documentSearch)}</div>
      ) : (
        <p>No document titles found...</p>
      )}

      <h1>Document Text Search</h1>
      {documentTextSearch.length ? (
        <div>{formatDocumentTextLinks(documentTextSearch)}</div>
      ) : (
        <p>No documents titles found...</p>
      )}
    </div>
  );
}

export default Search;
