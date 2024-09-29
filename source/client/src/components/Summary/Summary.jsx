import styles from "./Summary.module.scss";

function Summary() {
  return (
    <>
      <div className={styles.container}>
        <h2 className={styles.h2}>About First Last</h2>
        <p className={styles.body}>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ac
          vestibulum nunc. Nullam nec nunc nec libero ultricies tincidunt. Donec
          nec nunc nec libero ultricies tincidunt. Donec nec nunc nec libero
          ultricies tincidunt. Donec nec nunc nec libero ultricies tincidunt.
          Aliquam erat volutpat. Ut ac purus nec nunc nec libero ultricies. Ut
          enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi
          ut aliquip ex ea commodo consequat. Duis aute irure dolor in
          reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
          pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
          culpa qui officia deserunt mollit anim id est laborum.
        </p>
      </div>
      <div className={styles.container}>
        <h2 className={styles.h2}>About First Last's Interests</h2>
        <p className={styles.body}>
          Tempus congue vehicula etiam ultrices sodales tortor cras risus.
          Elementum molestie habitant suscipit sapien taciti felis curae proin.
          Sed magna dictum curae ut montes conubia pretium commodo. Aptent metus
          parturient praesent etiam enim lectus. Bibendum volutpat cubilia enim
          eros; consectetur egestas torquent netus. Montes cubilia pretium
          pretium egestas rutrum sapien blandit ipsum. Commodo aptent luctus
          dictum sed nec commodo maximus nisi.
        </p>
      </div>
    </>
  );
}

export { Summary };
