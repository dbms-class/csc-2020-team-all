// Copyright (C) 2019 Dmitry Barashev
package hellodb;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;

/**
 * @author dbms@barashev.net
 */
@Entity
public class Planet {
  @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
  Long id;
  String name;
}
