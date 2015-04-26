<?php
/**
 * plugin blankContentPlugin
 * @version 1.2
 * @package blankContentPlugin
 * @copyright Copyright (c) Jahr Firmennamen URL
 * @license http://www.gnu.org/copyleft/gpl.html GNU/GPL
 */

/**
 * Platz für Informationen
 * =======================
 *
 * Anwendung im Content:
 *   {BlankContentPlugin}
 *
 * Anwendung im Content mit Parameterübergabe:
 *   {BlankContentPlugin param1=Hello!|param2=it works fine|param3=Joomla! rocks ;-)}
 */


defined('_JEXEC') or die;

jimport('joomla.plugin.plugin');


class plgContentBlankContentPlugin extends JPlugin {


	function plgContentBlankContentPlugin( &$subject ) {
    parent::__construct( $subject );
  }


  /**
   * Contentstring Definition
   * String erkennen und mit neuem Inhalt füllen
   */
  public function onContentPrepare($context, &$article, &$params, $limitstart) {
		$regex = '/{BlankContentPlugin\s*(.*?)}/i';
		$article->text = preg_replace_callback($regex,array($this,"form"), $article->text);
	  return true;
  }


  public function form($matches) {

   /**
    * Contentstring zerlegen
    */
		$string = $matches[1];
    $params = explode('|',$string);


   /**
    * Parameter raus filtern und Variablen erstellen
    */
    foreach ($params as $param) {
      if (stristr($param,'param1=')) { $parameter1 = str_replace( 'param1=', '', $param ); }
      if (stristr($param,'param2=')) { $parameter2 = str_replace( 'param2=', '', $param ); }
      if (stristr($param,'param3=')) { $parameter3 = str_replace( 'param3=', '', $param ); }
      // kann beliebig erweitert werden
    }


   /**
    * individuelle Anwendung starten
    */
    $output = "<h3>Blank Content Plugin</h3>";
    if (isset($parameter1)) { $output .= "<h4>".$parameter1."</h4>"; }
    if (isset($parameter2)) { $output .= "<p>".$parameter2."</p>"; }
    if (isset($parameter3)) { $output .= "<p>".$parameter3."</p>"; }


    return $output;
	}

}

?>