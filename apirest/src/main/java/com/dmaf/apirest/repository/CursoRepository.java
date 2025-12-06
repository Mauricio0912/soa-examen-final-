package com.dmaf.apirest.repository;

import com.dmaf.apirest.model.Curso;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;
import java.util.List;

@Repository
public interface CursoRepository extends JpaRepository<Curso, Long> {

    List<Curso> findByNombreContainingIgnoreCase(String nombre);

    List<Curso> findByFechaInicio(LocalDate fechaInicio);
}
