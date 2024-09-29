import { useState } from "react";
import { Posts } from "../Posts/Posts";
import { Analytics } from "../Analytics/Analytics";
import { Summary } from "../Summary/Summary";
import styles from "./CenterColumn.module.scss";

function CenterColumn({ userId }) {
  const [selectedPage, setselectedPage] = useState("suggested");
  const updateSelectedPage = (page) => setselectedPage(page);
  return (
    <div className={styles.container}>
      <div className={styles.chips}>
        <div
          className={styles.green}
          onClick={() => updateSelectedPage("suggested")}
        >
          Suggested
        </div>
        <div
          className={styles.blue}
          onClick={() => updateSelectedPage("analytics")}
        >
          Analytics
        </div>
        <div
          className={styles.orange}
          onClick={() => updateSelectedPage("summary")}
        >
          Summary
        </div>
      </div>
      {selectedPage === "suggested" && <Posts userId={userId} />}
      {selectedPage === "analytics" && <Analytics />}
      {selectedPage === "summary" && <Summary />}
    </div>
  );
}

export { CenterColumn };
