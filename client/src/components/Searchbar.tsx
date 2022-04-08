import { Button, Input } from "antd";
import { SearchOutlined } from "@ant-design/icons";
import React, { useState } from "react";
import { useHistory } from "react-router";

export function Searchbar() {
  const [search, setSearch] = useState<string>();
  const history = useHistory();

  const onSearch = () => {
    if (!search) {
      // TODO - alert?
      return;
    }
    history.push({
      pathname: "/search",
      search: "?" + new URLSearchParams({ q: search }).toString(),
    });
  };

  return (
    <li style={{ order: 2, width: "100%" }}>
      <div className="items-center h-16 flex float-right pr-4 w-auto">
        <Input
          onChange={(e) => setSearch(e.target.value)}
          onPressEnter={onSearch}
          type="text"
          placeholder="SearchResults"
        />
        <Button onClick={onSearch} className="items-center">
          <SearchOutlined />
        </Button>
      </div>
    </li>
  );
}