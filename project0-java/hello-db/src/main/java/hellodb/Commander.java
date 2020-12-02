// Copyright (C) 2020 BarD Software
package hellodb;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.OneToMany;
import java.util.ArrayList;
import java.util.List;

@Entity(name = "commander")
public class Commander {
  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  Long id;

  String name;

  @OneToMany(
      mappedBy = "commander"
  )
  List<Flight> flights = new ArrayList<>();
}
